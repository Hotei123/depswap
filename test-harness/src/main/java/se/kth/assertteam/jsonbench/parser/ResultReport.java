package se.kth.assertteam.jsonbench.parser;

import se.kth.assertteam.jsonbench.ResultKind;

import java.util.ArrayList;
import java.util.List;

public class ResultReport {
    public ResultKind kind;
    public ArrayList<Long> memoryUsedList = new ArrayList<Long>();
    public Integer numberRuns = 1000;

    public ResultReport(){
        kind = null;
        for (int i = 0; i < numberRuns; i++) {
            memoryUsedList.add(0L);
        }
    }

    public void setPerformance(ResultKind kind, ArrayList<Long> memoryUsedList){
        this.kind = kind;
        this.memoryUsedList = memoryUsedList;
    }

}
