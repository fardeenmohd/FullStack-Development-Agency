package com.b2b.trade.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfig {

    @Value("${compute.engine.url}")
    private String computeEngineUrl;

    @Bean
    public WebClient computeWebClient(WebClient.Builder builder) {
        return builder
                .baseUrl(computeEngineUrl)
                .build();
    }
}