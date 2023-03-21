# %%
import time
import FlowManger


def main():
    flow_manger = FlowManger.FlowManger(time.time())
    flow_manger.population.genetic_algorithm()
    flow_manger.show_result()

    # best_individual, best_fitness = flow_manger.population.genetic_algorithm()
    # print("==============Final Result==================")
    # flow_manger.print_time()
    # print("Best individual:", ''.join(str(best_individual.gen)))
    # print("Best fitness:", best_fitness)
    return


if __name__ == "__main__":
    main()

# %%
