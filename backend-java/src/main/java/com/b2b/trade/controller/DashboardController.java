package com.b2b.trade.controller;

import com.b2b.trade.config.CustomUserDetails;
import com.b2b.trade.dto.MetricsResponse;
import com.b2b.trade.service.DashboardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/dashboard")
public class DashboardController {

    @Autowired
    private DashboardService dashboardService;

    @GetMapping("/metrics")
    public ResponseEntity<MetricsResponse> getMetrics(@AuthenticationPrincipal CustomUserDetails userDetails) {
        MetricsResponse metrics = dashboardService.getMetrics(userDetails.getUser());
        return ResponseEntity.ok(metrics);
    }
}