package com.example.springbootserver.controller.request;


/*
    Req8008
 */

public class Req8008  extends ReqBase{

    private String fut;

    private String start;

    private String end;

    private String shortT;

    private String longT;

    public String getFut() {
        return fut;
    }

    public String getStart() {
        return start;
    }

    public String getEnd() {
        return end;
    }

    public void setFut(String fut) { this.fut = fut; }

    public void setStart(String start) {
        this.start = start;
    }

    public void setEnd(String end) {
        this.end = end;
    }

    public void setLongT(String longT) {
        this.longT = longT;
    }

    public String getLongT() {
        return longT;
    }

    public String getShortT() {
        return shortT;
    }

    public void setShortT(String shortT) {
        this.shortT = shortT;
    }
}

