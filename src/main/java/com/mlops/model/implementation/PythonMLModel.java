package com.mlops.model.implementation;

import com.mlops.model.BaseModel;
import com.brokerage.utils.PythonCommands;

import java.util.Arrays;
import java.util.List;

public class PythonMLModel implements BaseModel {

    private static List<String> validCurrencies = Arrays.asList("AUD", "CHF", "EUR", "GBP", "JPY", "CAD", "MXP");

    private final String currency;

    public PythonMLModel(String currency) {
        this.currency = currency;
    }


    @Override
    public void train() throws Exception {
        PythonCommands.executeTrainModelPythonCommand(currency);
    }


    @Override
    public String predict(double open, double high, double low, double close, double volume, double wap, double count, double minute, double day, double month, double tesla3, double tesla6, double tesla9, double value5, double value6, String decision) throws Exception{
        return PythonCommands.executePredictModelCommand(String.valueOf(open), String.valueOf(high), String.valueOf(low), String.valueOf(close), String.valueOf(volume), String.valueOf(wap),
                String.valueOf(count), String.valueOf(minute), String.valueOf(day), String.valueOf(month), String.valueOf(tesla3), String.valueOf(tesla6), String.valueOf(tesla9),
                String.valueOf(value5), String.valueOf(value6), decision);
    }

    public static PythonMLModel getInstance(String currentSymbolFUT) throws Exception {
        if (validCurrencies.contains(currentSymbolFUT)) {
            PythonMLModel pythonMLModel = new PythonMLModel(currentSymbolFUT);
            pythonMLModel.train();
            return pythonMLModel;
        } else {
            throw new IllegalArgumentException("Not a valid currentSymbolFUT");
        }
    }
}
