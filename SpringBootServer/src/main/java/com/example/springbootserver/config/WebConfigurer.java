package com.example.springbootserver.config;

import org.springframework.boot.SpringBootConfiguration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@SpringBootConfiguration
public class WebConfigurer implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        WebMvcConfigurer.super.addCorsMappings(registry);

        registry.addMapping("/**")
//                .allowCredentials(true)
                .allowedOrigins("*")
                .allowedMethods("POST", "PUT", "OPTIONS", "DELETE", "GET")
                .allowedHeaders("*")
                .maxAge(3600);
    }
}
