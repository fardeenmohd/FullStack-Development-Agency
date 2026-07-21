package com.b2b.trade.service;

import com.b2b.trade.entity.Lead;
import com.b2b.trade.entity.User;
import com.b2b.trade.repository.LeadRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
public class LeadService {

    @Autowired
    private LeadRepository leadRepository;

    @Transactional(readOnly = true)
    public List<Lead> getLeadsForExporter(User exporter) {
        return leadRepository.findByExporter(exporter);
    }
}