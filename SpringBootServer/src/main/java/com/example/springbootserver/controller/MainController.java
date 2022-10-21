package com.example.springbootserver.controller;

import com.example.springbootserver.business.StrategistBusiness;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.example.springbootserver.tableDO.StrategistDO;

@Slf4j
@CrossOrigin
@RestController
public class MainController {

    @Autowired
    private StrategistBusiness stBiz;

    /**
     * 策略员登陆
     */
    @PostMapping(value = "/login")
    public ResponseEntity<Void> login(@RequestBody StrategistDO strategist) {
        log.info("login");
        boolean result = stBiz.ifLogin(strategist);
        return new ResponseEntity<>(result ? HttpStatus.OK : HttpStatus.BAD_REQUEST);
    }

    /**
     * 策略员注册
     */
    @PutMapping(value = "/register")
    public ResponseEntity<Void> add(@RequestBody StrategistDO strategist) {
        log.info("register");
        boolean result = stBiz.insertStrategist(strategist);
        return new ResponseEntity<>(result ? HttpStatus.OK : HttpStatus.BAD_REQUEST);
    }

    /**
     * 修改策略员密码/姓名
     */
    @PostMapping(value = "/modify")
    public ResponseEntity<Void> update(@RequestBody StrategistDO seat) {
        log.info("modify");
        boolean result = stBiz.updateStrategist(seat);
        return new ResponseEntity<>(result ? HttpStatus.OK : HttpStatus.BAD_REQUEST);
    }

    /**
     * 策略员注销
     */
    @RequestMapping(value = "/delete/{strategistId}", method = RequestMethod.DELETE)
    public ResponseEntity<Void> delete(@PathVariable("strategistId") int strategistId) {
        log.info("delete");
        boolean result = stBiz.deleteStrategist(strategistId);
        return new ResponseEntity<>(result ? HttpStatus.OK : HttpStatus.BAD_REQUEST);
    }
}
