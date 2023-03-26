# ID_1: 305283111
# ID_2: 207479940
import time
import FlowManger


def main():
    flow_manger = FlowManger.FlowManger(time.time())
    flow_manger.population.genetic_algorithm()
    flow_manger.show_result()

    return

if __name__ == "__main__":
    main()

# %%
