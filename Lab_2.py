# -----------Students ID -----------
# ID_1: 305283111
# ID_2: 207479940
# ----------- File For Genetic Algorithm -----------
import FlowManager
# ----------- Python Package -----------
import time


def main():
    flow_manager = FlowManager.FlowManager()
    # flow_manager.run_single_population_solution()
    flow_manager.run_multi_thread_population_solution()
    flow_manager.show_results()

    return


if __name__ == "__main__":
    main()
