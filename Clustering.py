# ----------- Python Package -----------
import math
import random
import numpy as np
# ----------- Consts Name  -----------
SHARED_FIT = 0
CLUSTER = 1
CROWDING = 2
SIGMA_SHARE = 2


def niche_algorithm(population: list, niche_algorithm_type):
    if niche_algorithm_type == SHARED_FIT:
        return shared_fitness_cluster(population)
    elif niche_algorithm_type == CLUSTER:
        return clustering(population)
    elif niche_algorithm_type == CROWDING:
        niches = []
        niches.append(population)
        return niches


def shared_fitness_cluster(population: list):
    similarity_matrix = similarity_matrix_init(population)
    niches = []
    for i, ind in enumerate(population):
        found_niche = False
        for niche in niches:
            for j, niche_ind in enumerate(niche):
                dist = similarity_matrix[i][j]
                if dist < SIGMA_SHARE:
                    niche.append(ind)
                    found_niche = True
                    break
            if found_niche:
                break
        if not found_niche:
            # If no niche found, create a new niche with the current individual
            niches.append([ind])

    return niches


def similarity_matrix_init(population: list):
    matrix = np.zeros((len(population), len(population)))
    for i in range(len(population)):
        for j in range(len(population)):
            matrix[i][j] = population[i].distance_func(population[j], True)

    return matrix


def clustering(population: list):
    silhouette_per_k = []
    elbow_method_per_k = []
    clusters_per_k = []
    max_clusters = 5
    for k in range(2, max_clusters):
        clusters_centers_update = []
        while True:
            clusters_centers_previous, clusters_previous = knn(k, population, clusters_centers_update)
            clusters_centers_update = update_clusters_centers(clusters_centers_previous, clusters_previous)
            clusters_centers_update, clusters_update = knn(k, population, clusters_centers_update)
            if equal_centers(clusters_centers_previous, clusters_centers_update):
                break

        clusters_per_k.append(clusters_update)
        silhouette_score = silhouette(clusters_centers_update, clusters_update)
        silhouette_per_k.append(silhouette_score)
        elbow_score = inertia(clusters_centers_update, clusters_update)
        elbow_method_per_k.append(elbow_score)

    max_silhouette_index = silhouette_per_k.index(max(silhouette_per_k))
    min_elbow_index = elbow_method_per_k.index(min(elbow_method_per_k))

    return clusters_per_k[max_silhouette_index]


def knn(k: int, population: list, clusters_centers: list):
    clusters = []
    clusters_centers_gen = []

    if not clusters_centers:
        while True:
            clusters_centers = random.sample(population, k)
            if valid_centers(clusters_centers):
                break

    for i in range(len(clusters_centers)):
        clusters.append([])

    for individual in population:
        if individual.gen not in clusters_centers_gen:
            dist = [individual.distance_func(center, True) for center in clusters_centers]
            min_dist_centers = []
            for index, center in enumerate(clusters_centers):
                if dist[index] == min(dist):
                    min_dist_centers.append((index, center))

            closest_center = random.sample(min_dist_centers, 1)[0]
            clusters[closest_center[0]].append(individual)
            # closest_center_index = dist.index(min(dist))
            # clusters[closest_center_index].append(individual)

    clusters_temp = clusters
    clusters_centers_temp = clusters_centers
    if len(clusters_temp) != len(clusters_centers_temp):
        print("clusters_temp:", len(clusters_temp))
        print("clusters_centers_temp:", len(clusters_centers_temp))
    for i, cluster in enumerate(clusters_temp):
        if len(cluster) == 0:
            clusters.remove(cluster)
            clusters_centers.remove(clusters_centers_temp[i])

    return clusters_centers, clusters


def valid_centers(clusters_centers: list):

    gens_centers = [center.gen for center in clusters_centers]
    for gen in gens_centers:
        count = 0
        for item in gens_centers:
            if gen == item:
                count += 1
            if count > 1:
                return False
    return True


def update_clusters_centers(clusters_centers: list, clusters: list):
    new_clusters_centers = []
    for cluster in clusters:
        cluster_fitness_pr = [individual.score * (1/len(cluster)) for individual in cluster]
        expectation = sum(cluster_fitness_pr)
        cluster_fitness = [individual.score - expectation for individual in cluster]
        new_center_index = cluster_fitness.index(min(cluster_fitness))
        new_clusters_centers.append(cluster[new_center_index])

    return new_clusters_centers


def equal_centers(clusters_centers_previous: list, clusters_centers_update: list):

    gens_clusters_centers_previous = [individual.gen for individual in clusters_centers_previous]
    gens_clusters_centers_update = [individual.gen for individual in clusters_centers_update]

    for gen in gens_clusters_centers_previous:
        if gen not in gens_clusters_centers_update:
            return False

    for gen in gens_clusters_centers_update:
        if gen not in gens_clusters_centers_previous:
            return False

    return True


def silhouette(clusters_centers: list, clusters: list):
    silhouette_score_cluster = []
    silhouette_score_all_clusters = []

    for index, cluster in enumerate(clusters):
        for individual in cluster:
            # Calculate the average distance between individual and all other points in cluster:
            dist_list = [individual.distance_func(ind, True) for ind in cluster]
            average_dist_in_cluster = sum(dist_list)/len(cluster)

            # Calculate the average distance between individual and all points in the nearest neighboring cluster
            nearest_cluster_index = find_nearest_cluster(individual, index, clusters_centers)
            dist_list = [individual.distance_func(ind, True) for ind in clusters[nearest_cluster_index]]
            average_dist_all_clusters = sum(dist_list)/len(clusters[nearest_cluster_index])

            # Calculate the silhouette score for individual
            silhouette_for_individual = (average_dist_all_clusters - average_dist_in_cluster) / max(average_dist_all_clusters, average_dist_in_cluster)
            silhouette_score_cluster.append(silhouette_for_individual)

        # The silhouette score for a cluster
        silhouette_for_cluster = sum(silhouette_score_cluster) / len(cluster)
        silhouette_score_all_clusters.append(silhouette_for_cluster)

    # The overall silhouette score for the clustering solution
    silhouette_score = sum(silhouette_score_all_clusters) / len(clusters)
    return silhouette_score


def find_nearest_cluster(individual, cluster_index, clusters_centers: list):
    dist_from_clusters = [individual.distance_func(center, True) for center in clusters_centers]
    nearest_cluster_index = 0
    nearest_cluster_dist = dist_from_clusters[0]
    for index, dist in enumerate(dist_from_clusters):
        if dist < nearest_cluster_dist and index != cluster_index:
            nearest_cluster_index = index
            nearest_cluster_dist = dist_from_clusters[index]

    return nearest_cluster_index


def inertia(species_centers, species):
    dist_per_cluster = []
    for index, cluster in enumerate(species):
        dist_list = [ind.distance_func(species_centers[index], True) for ind in cluster]
        dist_per_cluster.append(sum(dist_list) / len(cluster))

    average_dist_all_clusters = (sum(dist_per_cluster) / len(species))
    return average_dist_all_clusters




