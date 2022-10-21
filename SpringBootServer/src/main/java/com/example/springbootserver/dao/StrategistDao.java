package com.example.springbootserver.dao;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.example.springbootserver.mapper.StrategistMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import com.example.springbootserver.tableDO.StrategistDO;

@Component
public class StrategistDao {
    @Autowired
    private StrategistMapper strategistMapper;

    public boolean ifLogin(final StrategistDO strategist){
        QueryWrapper<StrategistDO> wrapper = new QueryWrapper<>();
        wrapper.eq("login_name", strategist.getLoginName());

        StrategistDO st = strategistMapper.selectOne(wrapper);
        if(st != null && st.getPassword().equals(strategist.getPassword())) {
            // 允许登陆
            System.out.println("允许登陆");
            return true;
        }
        return false;
    }

    public boolean insertStrategist(final StrategistDO strategist) {
        return strategistMapper.insert(strategist)>0;
    }

    public boolean updateStrategist(final StrategistDO strategist) {
        QueryWrapper<StrategistDO> wrapper = new QueryWrapper<>();

        wrapper.eq("login_name", strategist.getLoginName());
        return strategistMapper.update(strategist, wrapper)>0;
    }

    public boolean deleteStrategist(final int strategistId) {
        QueryWrapper<StrategistDO> wrapper = new QueryWrapper<>();
        wrapper.le("login_name", strategistId);
        return strategistMapper.delete(wrapper)>0;
    }
}
