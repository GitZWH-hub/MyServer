package com.example.springbootserver.controller;

import cn.hutool.json.JSONObject;
import com.example.springbootserver.controller.request.ReqPy8100;
import com.example.springbootserver.controller.request.ReqPy9000;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import javax.websocket.*;
import javax.websocket.server.ServerEndpoint;
import java.io.IOException;
import org.springframework.web.bind.annotation.PostMapping;
import java.util.Set;
import java.util.concurrent.CopyOnWriteArraySet;

@ServerEndpoint("/ws")
@Component("SpringBootServer")
@Slf4j
@RestController
public class WebSocketServer {

    private static String url = "http://localhost:3001/request";

    /* 多连接 concurrent包的线程安全Set，用来存放每个客户端对应的MyWebSocket对象
    private static final CopyOnWriteArraySet<WebSocketServer> webSocketSet = new CopyOnWriteArraySet<>();
    public static Set<WebSocketServer> getWebSocketSet() {
        return webSocketSet;
    }
    */

    private static WebSocketServer webSocketSet = new WebSocketServer();
    public static WebSocketServer getWebSocketSet(){return webSocketSet;}

    private Session session;

    @OnOpen
    public void onOpen(Session session) throws IOException {
        this.session = session;
        /*webSocketSet.add(this);*/
        webSocketSet = this;
        log.info("系统连接成功");
    }

    @OnClose
    public void onClose() {
        /*webSocketSet.remove(this);*/
        webSocketSet = null;
        log.info("断开连接");
    }

    @OnError
    public void onError(Session session, Throwable error) {
        log.info("断开连接");
    }

    /**
     * 收到客户端消息后调用的方法
     */
    @OnMessage
    public void onMessage(String message) {
        log.info("用户消息");
        try {
            JSONObject postData = new JSONObject(message);
            log.info(String.valueOf(postData));
            RestTemplate client = new RestTemplate();
            // 发送给Python服务
            JSONObject json = client.postForEntity(url, postData, JSONObject.class).getBody();
            log.info(String.valueOf(json));
        }catch (Exception e){
            e.printStackTrace();
        }
    }

    /*
    * 【Python】 to 【Java】 to 【Client】
    * */
    @ApiOperation("Python发送消息sendBack")
    @PutMapping("/sendBack")
    public String sendBack(@RequestBody ReqPy8100 req) throws IOException {
        System.out.println("收到py请求返回给客户端");
        JSONObject payInfoJsonObject = new JSONObject(req);
        String str = payInfoJsonObject.toString();
        log.info(str);
        sendMessage(str);
        return "success";
    }
    /*
     * 【Python】 to 【Java】 to 【Client】
     * */
    @ApiOperation("Python发送消息sendHTML")
    @PutMapping("/sendHTML")
    public String sendHTML(@RequestBody ReqPy9000 req) throws IOException {
        log.info("收到py请求返回给客户端");
        JSONObject payInfoJsonObject = new JSONObject(req);
        String str = payInfoJsonObject.toString();
        log.info(str);
        sendMessage(str);
        return "success";
    }


    /**
     * 实现服务器主动推送
     */
    public void sendMessage(String message) throws IOException {
        if (webSocketSet.session.isOpen()) {
            webSocketSet.session.getBasicRemote().sendText(message);
        }

        /*
        for (WebSocketServer item : webSocketSet) {
            if (item.session.isOpen()) {
                item.session.getBasicRemote().sendText(message);
            }
        }
        */
    }

}




/*
*   群发消息
    for (MotorAlarmWebSocketServer item : webSocketSet) {
        try {
            item.sendMessage(message);
        } catch (IOException e) {
            log.info("消息发送失败");
        }
    }
* */

/* 追加发送人(防止串改)
    jsonObj.put("fromUserId", userid);
    String toUserId = jsonObj.get("toUserId").toString();
    // 传送给对应UserId用户的websocket
    if(toUserId != null && webSocketSet.contains(toUserId)){
    this.sendMessage(jsonObj.toJSONString());
    }else{
    log.error("请求的userId:"+toUserId+"不在该服务器上");
    //否则不在这个服务器上，发送到mysql或者redis
    }
*/

