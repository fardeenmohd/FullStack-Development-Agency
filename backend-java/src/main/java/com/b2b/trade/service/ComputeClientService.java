package com.b2b.trade.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import java.util.Map;
import java.util.UUID;

@Service
public class ComputeClientService {

    @Autowired
    private WebClient computeWebClient;

    public Mono<Void> triggerHuntLeads(UUID productId) {
        return computeWebClient.post()
                .uri("/api/v1/compute/hunt-leads")
                .bodyValue(Map.of("productId", productId.toString()))
                .retrieve()
                .bodyToMono(Void.class);
    }

    public Mono<Void> triggerScoreLead(UUID leadId) {
        return computeWebClient.post()
                .uri("/api/v1/compute/score-lead")
                .bodyValue(Map.of("leadId", leadId.toString()))
                .retrieve()
                .bodyToMono(Void.class);
    }
}