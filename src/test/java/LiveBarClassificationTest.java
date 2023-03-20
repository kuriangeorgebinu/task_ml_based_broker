import com.brokerage.strategy.LiveBarPriorClassification;


public class LiveBarClassificationTest {


    public static void testExecuteOrNot() {
        String currency = "AUD";
        double open =0.6656;
        double high =0.66565;
        double low = 0.6647;
        double close = 0.6648;
        int volume = 407;
        double wap = 0.665085;
        int count= 188;
        double minute= 45;
        double day= 32;
        double month= 1.052054795;
        double tesla3= -0.000741;
        double tesla6= -0.001719;
        double tesla9= -0.002862;
        double value5= 9;
        double value6= 2;
        String decision = "SELL";

        LiveBarPriorClassification liveBarPriorClassification = new LiveBarPriorClassification(open, high, low, close,volume, wap, count, minute, day, month, tesla3, tesla6, tesla9, value5, value6, decision);
        String executeOrNot = liveBarPriorClassification.executeOrNot(currency);
        System.out.println("The Decision is "+executeOrNot);
    }

    public static void main(String [] args) {
        testExecuteOrNot();
    }


}
