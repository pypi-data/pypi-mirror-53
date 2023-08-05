from differentialevolution import DifferentialEvolution as DE
from pop import Population


def main():
    de = DE(Population, population_size=50, generations=5000, CR=0.3)
    de.search()
    de.plot_history()


if __name__ == "__main__":
    main()
