#include <omp.h>
#include <random>
#include <cmath>
#include "ncvis.hpp"
#include "../lib/pcg-cpp/include/pcg_random.hpp"
#include <chrono>

ncvis::NCVis::NCVis(long d, long n_threads, long n_neighbors, long M, 
                    long ef_construction, long random_seed, int n_epochs, 
                    int n_init_epochs, float a, float b, float alpha, float alpha_Q, long* n_noise, ncvis::Distance dist):
d_(d), M_(M), ef_construction_(ef_construction), 
random_seed_(random_seed), n_neighbors_(n_neighbors), n_epochs_(n_epochs), n_init_epochs_(n_init_epochs), a_(a), b_(b), alpha_(alpha), alpha_Q_(alpha_Q), space_(nullptr), appr_alg_(nullptr), dist_(dist)
{
    omp_set_num_threads(n_threads);
    n_noise_ = new long[n_epochs];
    long default_noise = 3;
    for (int i=0; i<n_epochs; ++i){
        n_noise_[i] = (n_noise == nullptr)? default_noise:n_noise[i];
    }
}

ncvis::NCVis::~NCVis(){
    delete space_;
    space_ = nullptr;
    delete appr_alg_;
    appr_alg_ = nullptr;
    delete[] n_noise_;
    n_noise_ =  nullptr;
}

void ncvis::NCVis::preprocess(const float *const x, long D, ncvis::Distance dist, float* out){
    if (dist == ncvis::Distance::correlation){
        float M = 0;
        for (long i = 0; i < D; ++i){
            M += x[i];
        }
        M /= D;
        // printf("[ncvis::NCVis::preprocess] M = %f\n", M);
        for (long i = 0; i < D; ++i){
            out[i] = x[i]-M;
        }
    }
    else{
        for (long i = 0; i < D; ++i){
            out[i] = x[i];
        }
    }
    // printf("[ncvis::NCVis::preprocess](center) [");
    // for (long j=0; j<D; ++j){
    //     printf("%5.1f ", out[j]);
    // }
    // printf("]\n");
    if (dist == ncvis::Distance::correlation || dist == ncvis::Distance::cosine_similarity){
        float N = 0;
        for (long i = 0; i < D; ++i){
            N += out[i]*out[i];
        }
        // printf("[ncvis::NCVis::preprocess] N = %f\n", sqrtf(N));
        if (N != 0){
            for (long i = 0; i < D; ++i){
                out[i] /= sqrtf(N);
            }
        }
    }
    // printf("[ncvis::NCVis::preprocess](norm) [");
    // for (long j=0; j<D; ++j){
    //     printf("%5.1f ", out[j]);
    // }
    // printf("]\n");
}

void ncvis::NCVis::buildKNN(const float *const X, long N, long D){
    delete space_;
    space_ = nullptr;
    delete appr_alg_;
    appr_alg_ = nullptr;

    switch(dist_){
        case ncvis::Distance::squared_L2:
            // printf("[ncvis::NCVis::buildKNN] squared_L2\n");
            space_ = new hnswlib::L2Space(D);
            break;
        case ncvis::Distance::inner_product:
        case ncvis::Distance::cosine_similarity:
        case ncvis::Distance::correlation:
            // printf("[ncvis::NCVis::buildKNN] inner_product || cosine_similarity || correlation\n");
            space_ = new hnswlib::InnerProductSpace(D);
            break;
        default: 
            throw std::runtime_error("[ncvis::NCVis::buildKNN] Unrecognized distance type.");
            break;
    }
    appr_alg_ = new hnswlib::HierarchicalNSW<float>(space_, N, M_, ef_construction_, random_seed_);

    // Perform initialisation without messing with mutexes 
    float* x = new float[D];
    preprocess(X, D, dist_, x);
    appr_alg_->addPoint((void*)x, 0);
    delete[] x;

    #pragma omp parallel
    {
    float* x = new float[D];
    #pragma omp for
    for (long i=1; i < N; ++i){
        // printf("[%lu]>> [", i);
        // for (long j=0; j<D; ++j){
        //     printf("%5.1f ", X[j+D*i]);
        // }
        // printf("]\n");
        preprocess(X+i*D, D, dist_, x);
        // printf("[%lu]<< [", i);
        // for (long j=0; j<D; ++j){
        //     printf("%5.1f ", x[j]);
        // }
        // printf("]\n");
        appr_alg_->addPoint((void*)x, i);
    }
    delete[] x;
    }
}

ncvis::KNNTable ncvis::NCVis::findKNN(const float *const X, long N, long D, long k){
    KNNTable table(N, k);

    #pragma omp parallel
    {
    float* x = new float[D];
    #pragma omp for
    for (long i=0; i < N; ++i){
        // Find k+1 neighbors as one of them is the point itself
        preprocess(X+i*D, D, dist_, x);
        auto result = appr_alg_->searchKnn((const void*)x, k+1);
        if ((long)result.size() != k+1){
            std::cout << "[ncvis::NCVis::findKNN] Found less than k nearest neighbors, try increasing M or ef_construction.";
        } else{
            for (long j=0; j<k; ++j) {
                auto& result_tuple = result.top();
                table.dists[i].push_back(result_tuple.first);
                table.inds[i].push_back(result_tuple.second);
                result.pop();
            }
        }
    }
    delete[] x;
    }

    return table;
}

void ncvis::NCVis::build_edges(ncvis::KNNTable& table){
    long n_edges = 0;

    #pragma omp parallel for
    for (long i = 0; i < (long)table.inds.size(); ++i){
        #pragma omp atomic
        n_edges += (long)table.inds[i].size();
    }
    edges_.reserve(n_edges);

    for (long i = 0; i < (long)table.inds.size(); ++i){
        for (long j =0; j < (long)table.inds[i].size(); ++j){
            edges_.emplace_back(i, table.inds[i][j]);
        }
    }
}

float ncvis::NCVis::d_sqr(const float *const x, const float *const y){
    float dist_sqr = 0;
    for (long i = 0; i < d_; ++i){
        dist_sqr += (x[i]-y[i])*(x[i]-y[i]);
    }

    return dist_sqr;
}

void ncvis::NCVis::init_embedding(long N, float*& Y, float alpha){
    // For temporary values 
    float* Y_swap = new float[N*d_];
    float* mean = new float[d_];
    float* sigma = new float[d_];

    #pragma omp parallel
    {
    pcg64 pcg(random_seed_+omp_get_thread_num());
    std::uniform_real_distribution<float> gen_Y(0, 1);

    #pragma omp for
    for (long i = 0; i < N*d_; ++i){
        Y[i] = gen_Y(pcg);
    }

    // Initialize layout
    for (int init_epoch = 0; init_epoch < n_init_epochs_; ++init_epoch){
        #pragma omp single
        {
        float* tmp = Y_swap;
        Y_swap = Y;
        Y = tmp;
        }
        #pragma omp for
        for (long i = 0; i < N*d_; ++i){
            Y[i] = 0;
        }
        #pragma omp for
        for (long i = 0; i < (long)edges_.size(); ++i){
            long id = edges_[i].first;
            long other_id = edges_[i].second;
            
            for (long k = 0; k < d_; ++k){
                // float dx_k = Y[other_id*d_+k] - Y[id*d_+k];
                // dx_k = dx_k * init_alpha;
                // printf("dx[%ld] = %f\n", k, dx_k);
                // Y[id*d_+k] += dx_k;
                // Y[other_id*d_+k] -= dx_k;
                Y[id*d_+k] += alpha * Y_swap[other_id*d_+k];
            }
        }

        #pragma omp single
        for (long k = 0; k < d_; ++k){
            mean[k] = 0;
            sigma[k] = 0;
        }

        #pragma omp for
        for (long i = 0; i < N; ++i){
            for (long k = 0; k < d_; ++k){
                #pragma omp atomic
                mean[k] += Y[i*d_+k];
            }
        }

        #pragma omp single
        for (long k = 0; k < d_; ++k){
            mean[k] /= N;
        }

        #pragma omp for
        for (long i = 0; i < N; ++i){
            for (long k = 0; k < d_; ++k){
                #pragma omp atomic
                sigma[k] += (Y[i*d_+k] - mean[k])*(Y[i*d_+k] - mean[k]);
            }
        }

        #pragma omp single
        for (long k = 0; k < d_; ++k){
            sigma[k] /= N;
            sigma[k] = sqrtf(sigma[k]);
        }

        #pragma omp for
        for (long i = 0; i < N; ++i){
            for (long k = 0; k < d_; ++k){
                Y[i*d_+k] = (Y[i*d_+k] - mean[k])/sigma[k];
            }
        }
    }
    }
    
    delete[] Y_swap;
    delete[] mean;
    delete[] sigma;
}

void ncvis::NCVis::optimize(long N, float* Y, float& Q){
    float Q_cum=0.;
    #pragma omp parallel
    {
    pcg64 pcg(random_seed_+omp_get_thread_num());
    // Build layout
    std::uniform_int_distribution<long> gen_ind(0, N-1);

    for (int epoch = 0; epoch < n_epochs_; ++epoch){
        // Hogwild: lock-free parameters reading and writing
        float step = alpha_*(1-(((float)epoch)/n_epochs_)*(((float)epoch)/n_epochs_));
        float Q_copy = Q;
        long cur_noise = n_noise_[epoch];
        Q_cum = 0;
        #pragma omp for
        for (long i = 0; i < (long)edges_.size(); ++i){
            // printf("[%d] (%ld, %ld)\n", epoch, edges_[i].first, edges_[i].second);
            long id = edges_[i].first;
            for (long j = 0; j < cur_noise+1; ++j){
                long other_id;
                if (j == 0){
                    other_id = edges_[i].second; 
                } else{
                    do{
                        other_id = gen_ind(pcg);
                    } while (other_id == id);
                }

                float d2 = d_sqr(Y+id*d_, Y+other_id*d_);
                float Ph = 1/(1+a_*powf(d2, b_));
                float w = 1.;
                if (cur_noise != 0){
                    w = Ph/(cur_noise*expf(Q_copy));
                    // w = Ph/(cur_noise*expf(Q));
                    if (j == 0){
                        w = 1/(1+w);    
                    } else {
                        w = -1/(1+1/w);
                    }
                    // Non-blocking write
                    // #pragma omp critical
                    // {
                    // printf("[%d:%d] Ph = %f\n", epoch, omp_get_thread_num(), Ph);
                    // }
                    Q_copy -= w*alpha_Q_;
                    // Q -= w*alpha_Q;
                    w = 2*w*Ph*a_*b_*powf(d2, b_-1);
                }
                // #pragma omp critical
                // {
                // printf("[%d:%d] Q = %f\n", epoch, omp_get_thread_num(), Q);
                // }
                // Also non-blocking write
                for (long k = 0; k < d_; ++k){
                    float dx_k = Y[other_id*d_+k] - Y[id*d_+k];
                    dx_k = dx_k * w * step;
                    if (dx_k > 4.){
                        dx_k = 4.;
                    } else if (dx_k < -4.){
                        dx_k = -4.;
                    }
                    Y[id*d_+k] += dx_k;
                    Y[other_id*d_+k] -= dx_k;
                }
            }  
        }
        #pragma omp critical
        Q_cum += Q_copy;
        #pragma omp single
        Q = Q_cum/omp_get_num_threads();
    }
    }
}

float* ncvis::NCVis::fit_transform(const float *const X, long N, long D){
    // printf("==============DATA============\n");
    // for (long i=0; i<N; ++i){
    //     printf("[");
    //     for (long j=0; j<D; ++j){
    //         printf("%5.2f ", X[j+D*i]);
    //     }
    //     printf("]\n");
    // }
    // printf("===============================\n");
    if (N == 0 || D == 0){ 
        throw std::runtime_error("[ncvis::NCVis::fit_transform] Dataset should have at least one element.");
        return nullptr;
    }
    #if defined(DEBUG)
        auto t1 = std::chrono::high_resolution_clock::now();
        buildKNN(X, N, D);
        auto t2 = std::chrono::high_resolution_clock::now();
        std::cout << "buildKNN: "
                  << std::chrono::duration_cast<std::chrono::milliseconds>(t2-t1).count()
                  << " ms\n";
    #else 
        buildKNN(X, N, D);
    #endif
    // Number of neighbors can't exceed the total number of other points 
    long k = (n_neighbors_ < N-1)? n_neighbors_:(N-1);
    k = (k > 0)? k:1;
    #if defined(DEBUG)
        t1 = std::chrono::high_resolution_clock::now();
        KNNTable table = findKNN(X, N, D, k);
        
        // The graph itself is no longer needed
        delete appr_alg_;
        appr_alg_ = nullptr;
        delete space_;
        space_ = nullptr;

        t2 = std::chrono::high_resolution_clock::now();
        std::cout << "findKNN: "
                << std::chrono::duration_cast<std::chrono::milliseconds>(t2-t1).count()
                << " ms\n";
        t1 = std::chrono::high_resolution_clock::now();
        table.symmetrize();
        t2 = std::chrono::high_resolution_clock::now();
        std::cout << "symmetrize: "
                << std::chrono::duration_cast<std::chrono::milliseconds>(t2-t1).count()
                << " ms\n";
        t1 = std::chrono::high_resolution_clock::now();
        build_edges(table);
        t2 = std::chrono::high_resolution_clock::now();
        std::cout << "build_edges: "
                << std::chrono::duration_cast<std::chrono::milliseconds>(t2-t1).count()
                << " ms\n";
    #else
        KNNTable table = findKNN(X, N, D, k);

        // The graph itself is no longer needed
        delete appr_alg_;
        appr_alg_ = nullptr;
        delete space_;
        space_ = nullptr;

        table.symmetrize();
        build_edges(table);
    #endif

    // Likelihood parameters
    float* Y = new float[N*d_];
    // Normalization
    float Q=0.;
    float init_alpha = 1./k;
    
    #if defined(DEBUG)
        t1 = std::chrono::high_resolution_clock::now();
    #endif

    init_embedding(N, Y, init_alpha);
    optimize(N, Y, Q);
    
    #if defined(DEBUG)
        t2 = std::chrono::high_resolution_clock::now();
        std::cout << "main cycle: "
                << std::chrono::duration_cast<std::chrono::milliseconds>(t2-t1).count()
                << " ms\n";
    #endif
    // printf("============DISTANCES==========\n");
    // for (long i=0; i<N; ++i){
    //     printf("[");
    //     for (long j=0; j<table.dists[i].size(); ++j){
    //         printf("%f ", table.dists[i][j]);
    //     }
    //     printf("]\n");
    // }
    // printf("===============================\n");

    // printf("============NEIGHBORS==========\n");
    // for (long i=0; i<N; ++i){
    //     printf("[");
    //     for (long j=0; j<table.inds[i].size(); ++j){
    //         printf("%ld ", table.inds[i][j]);
    //     }
    //     printf("]\n");
    // }
    // printf("===============================\n");

    return Y;
}