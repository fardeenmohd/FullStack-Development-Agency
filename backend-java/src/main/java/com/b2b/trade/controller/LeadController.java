package com.b2b.trade.controller;

import com.b2b.trade.config.CustomUserDetails;
import com.b2b.trade.entity.Lead;
import com.b2b.trade.service.LeadService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@RestController
@RequestMapping("/api/v1/leads")
public class LeadController {

    @Autowired
    private LeadService leadService;

    @GetMapping
    @PreAuthorize("hasRole('EXPORTER')")
    public ResponseEntity<List<Lead>> getLeads(@AuthenticationPrincipal CustomUserDetails userDetails) {
        List<Lead> leads = leadService.getLeadsForExporter(userDetails.getUser());
        return ResponseEntity.ok(leads);
    }
}