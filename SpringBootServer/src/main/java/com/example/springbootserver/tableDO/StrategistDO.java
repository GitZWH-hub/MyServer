package com.example.springbootserver.tableDO;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import javax.persistence.*;

@Data
@Entity
@Table(name="Strategist")
@TableName("Strategist")
public class StrategistDO {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @TableId(type = IdType.INPUT)
    @Column(columnDefinition="bigint(20) comment '登陆用户名'")
    private Integer loginName;

    @Column(columnDefinition="varchar(20) comment '登录密码'")
    private String password;

    @Column(columnDefinition="varchar(20) comment '策略员姓名'")
    private String name;

}
