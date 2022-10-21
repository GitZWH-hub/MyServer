package com.example.springbootserver.business;

import com.example.springbootserver.dao.StrategistDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import com.example.springbootserver.tableDO.StrategistDO;


@Component
public class StrategistBusiness {
    @Autowired
    private StrategistDao strategistDao;

    public boolean ifLogin(final StrategistDO strategist){
        return strategistDao.ifLogin(strategist);
    }

    public boolean insertStrategist(final StrategistDO strategist) {
        return strategistDao.insertStrategist(strategist);
    }

    public boolean updateStrategist(final StrategistDO strategist) {
        return strategistDao.updateStrategist(strategist);
    }

    public boolean deleteStrategist(final int strategistId) {
        return strategistDao.deleteStrategist(strategistId);
    }
}
