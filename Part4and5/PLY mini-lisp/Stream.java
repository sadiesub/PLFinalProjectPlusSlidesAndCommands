import java.util.*;
public class Stream {

    public static double streamIt(int number, int... numbers){
        ArrayList<Integer> a1 = new ArrayList<Integer>();
        ArrayList<Integer> endResult = new ArrayList<Integer>();
        a1.add(number);
        for(int u: numbers){a1.add(u);}
        //a1
        //        .stream()
        //        .filter(e -> e >= 70)
        //        .forEach(e -> endResult.add(e));

        double avg = a1
                .stream()
                .filter(e -> e >= 70)
                .mapToInt(e -> e)
                .average()
                .getAsDouble();

        return avg;

    }

}