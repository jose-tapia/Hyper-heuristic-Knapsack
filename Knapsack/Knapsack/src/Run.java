
import HERMES.Exceptions.NoSuchHeuristicException;
import KP.Solvers.Constructive.ConstructiveSolver;
import KP.KnapsackProblem;
import KP.KnapsackProblemSet;
import KP.KnapsackProblemSet.Subset;
import KP.Solvers.HyperHeuristic.SampleHyperHeuristic;

public class Run {

    public static void main(String[] args) {

        String[] features, heuristics;
        KnapsackProblem[] problems;
        KnapsackProblemSet trainingSet, testSet;
        ConstructiveSolver solver;
        SampleHyperHeuristic hh;
        StringBuilder string;

        /*
            Available features.
        */
        features = new String[]{
            "NORM_CORRELATION",};

        /*
            Available heuristics.
        */
        heuristics = new String[]{
            "MIN_WEIGHT",
            "MAX_PROFIT",
            "MAX_PROFIT_PER_WEIGHT_UNIT",
            "MAX_PROFIT2_PER_WEIGHT_UNIT",
            "MAX_PROFIT_PER_WEIGHT_UNIT2",
            "AVG_PROFIT"
        };

        /*
         * Creates the training and test sets (60 and 40% of the original data, respectively).
         */
        trainingSet = new KnapsackProblemSet("../kplib/", Subset.TRAIN, 0.60, 12345);
        testSet = new KnapsackProblemSet("../kplib/", Subset.TEST, 0.60, 12345);        
        
        /*
            Solves all the instances in the training set. 
            You can change the set to solve all the instances in the test set.
            This code uses all the heuristics defined before.
        */
        problems = trainingSet.getInstances();
        string = new StringBuilder();
        for (String heuristic : heuristics) {
            string.append(heuristic).append("\t");
        }
        System.out.println(string.toString());
        for (KnapsackProblem problem : problems) {
            string = new StringBuilder();
            for (int j = 0; j < heuristics.length; j++) {
                solver = new ConstructiveSolver(problem);
                try {
                    solver.solve(solver.getHeuristic(heuristics[j]));
                    string.append(solver.getProfit()).append("\t");
                } catch (NoSuchHeuristicException exception) {
                    System.out.println(exception);
                    System.exit(1);
                }
            }
            System.out.println(string.toString());
        }
    }

}
