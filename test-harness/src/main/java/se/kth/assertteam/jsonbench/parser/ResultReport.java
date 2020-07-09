package se.kth.assertteam.jsonbench.parser;

import se.kth.assertteam.jsonbench.ResultKind;

public class ResultReport {
    public ResultKind kind;
    public long memoryUsed;

    public ResultReport(){
        kind = null;
        memoryUsed = 0;
    }

    public void setPerformance(ResultKind kind, long memoryUsed){
        kind = kind;
        memoryUsed = memoryUsed;
    }

}
