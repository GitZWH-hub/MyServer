package com.example.springbootserver.controller.request;

public class ReqPy9000 {

    /*
    *  是否成功生成数据的html
    * '1': 生成成功   '-1'：生成失败
    */
    private String if_get;

    /*
    * 生成html的合约代码
    */
    private String ts_code;

    public String getTs_code() {
        return ts_code;
    }

    public void setTs_code(String ts_code) {
        this.ts_code = ts_code;
    }

    public void setIf_get(String if_get) {
        this.if_get = if_get;
    }

    public String getIf_get() {
        return if_get;
    }
}
