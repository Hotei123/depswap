package se.kth.assertteam.jsonbench.parser;

import se.kth.assertteam.jsonbench.ResultKind;

public class ResultReport {
    public
        ResultKind kind;
        int memoryUsed;

    public ResultReport(){
        kind = null;
        memoryUsed = 0;
    }
}
