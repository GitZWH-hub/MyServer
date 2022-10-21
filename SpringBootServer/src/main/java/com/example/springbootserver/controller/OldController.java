package com.example.springbootserver.controller;

import cn.hutool.http.HttpUtil;
import cn.hutool.json.JSONObject;
import com.example.springbootserver.controller.request.*;
import io.swagger.annotations.ApiOperation;
import lombok.extern.java.Log;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

@Slf4j
@CrossOrigin
@RestController
public class OldController {

    private String host = "http://localhost:3001/short";

    /*
     * 8001：查询交易所下所有期货代码
     * */
    @PostMapping("/Req8001")
    public String getKData(@RequestBody Req8001 req){
        log.info("Req8001");
        JSONObject payInfoJsonObject = new JSONObject(req);
        log.info(payInfoJsonObject.toString());
        return HttpUtil.post(host, payInfoJsonObject.toString());
    }

    /*
     * 8002: 拉取数据
     * */
    @PostMapping("/Req8002")
    public String pullData(@RequestBody Req8002 req) {
        log.info("Req8002");
        JSONObject payInfoJsonObject = new JSONObject(req);
        return HttpUtil.post(host, payInfoJsonObject.toString());
    }

    /*
     * 8008: 回测拉取数据
     * */
    @PostMapping("/Req8008")
    public String BackTestPull(@RequestBody Req8008 req) {
        log.info("Req8008");
        JSONObject payInfoJsonObject = new JSONObject(req);
        return HttpUtil.post(host, payInfoJsonObject.toString());
    }

    /*
     * 8003: 查看股票信息
     * */
    @PostMapping("/Req8003")
    public String selectStock(@RequestBody Req8003 req) {
        log.info("Req8003");
        JSONObject payInfoJsonObject = new JSONObject(req);
        return HttpUtil.post(host, payInfoJsonObject.toString());
    }
}
