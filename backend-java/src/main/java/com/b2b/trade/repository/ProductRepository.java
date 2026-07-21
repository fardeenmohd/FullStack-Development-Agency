package com.b2b.trade.repository;

import com.b2b.trade.entity.Product;
import com.b2b.trade.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.UUID;

public interface ProductRepository extends JpaRepository<Product, UUID> {
    List<Product> findByExporter(User exporter);
}