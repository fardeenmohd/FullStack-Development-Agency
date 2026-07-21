package com.app.service;

import com.app.model.Lead;
import com.app.repository.LeadRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class LeadService {
    @Autowired
    private LeadRepository leadRepository;

    public Lead saveLead(Lead lead) {
        return leadRepository.save(lead);
    }
}
