package com.example.springbootserver.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.springframework.stereotype.Component;
import com.example.springbootserver.tableDO.StrategistDO;

@Component(value = "StrategistMapper")
public interface StrategistMapper extends BaseMapper<StrategistDO> {
}
