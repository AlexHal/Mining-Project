import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Map;
import java.util.LinkedHashMap;
import java.util.concurrent.*;
import java.util.regex.*;

public class run_concurrently {

    public static void main(String[] args) throws Exception {

        if (args.length < 2) {
            System.out.println("Usage: java run_concurrently <numRuns> <numThreads> [pythonCmd]");
            return;
        }

        int numRuns = Integer.parseInt(args[0]);
        int numThreads = Integer.parseInt(args[1]);
        String pythonCmd = args.length >= 3 ? args[2] : "python";

        ExecutorService pool = Executors.newFixedThreadPool(numThreads);

        ConcurrentLinkedQueue<Map<String, Double>> results = new ConcurrentLinkedQueue<>();

        for (int i = 0; i < numRuns; i++) {

            final int runId = i + 1;

            pool.submit(() -> {
                try {
                    //Build python program
                    ProcessBuilder pb = new ProcessBuilder(pythonCmd, "DRS_Simulator.py");
                    pb.redirectErrorStream(true);

                    Process p = pb.start();
                    
                    // Read and store python program output
                    BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));
                    
                    StringBuilder out = new StringBuilder();
                    String line;

                    while ((line = r.readLine()) != null)
                        out.append(line).append('\n');

                    // wait for process to terminate
                    int rc = p.waitFor();

                    if (rc != 0)
                        throw new RuntimeException("Run " + runId + " failed");
                    // Parse
                    Map<String, Double> stats = parseStats(out.toString());

                    if (!stats.isEmpty())
                        results.add(stats);

                } catch (Exception e) {
                    System.err.println("Run " + runId + " failed: " + e.getMessage());
                }
            });
        }

        pool.shutdown();

        Map<String, Double> sums = new LinkedHashMap<>();
        int success = 0;
        // Sum data from all runs, count how many worked
        for (Map<String, Double> res : results) {
            for (Map.Entry<String, Double> e : res.entrySet()) {
                sums.merge(e.getKey(), e.getValue(), Double::sum);
            }
            success++;
        }

        if (success == 0) {
            System.err.println("No successful runs.");
            System.exit(2);
        }

        System.out.println("Completed " + success + " runs. Averages:");
        // Print avgs
        for (Map.Entry<String, Double> e : sums.entrySet()) {
            System.out.printf("%s: %.6f\n", e.getKey(), e.getValue() / success);
        }
    }

    // Parser, generated
    private static Map<String, Double> parseStats(String out) {

        Map<String, Double> m = new LinkedHashMap<>();

        Pattern p = Pattern.compile(
            "^\\s*([^:]+):\\s*([+-]?[0-9]*\\.?[0-9]+(?:[eE][+-]?[0-9]+)?)\\s*$",
            Pattern.MULTILINE
        );

        Matcher mt = p.matcher(out);

        while (mt.find()) {
            String key = mt.group(1).trim();
            double val = Double.parseDouble(mt.group(2));
            m.put(key, val);
        }

        return m;
    }
}