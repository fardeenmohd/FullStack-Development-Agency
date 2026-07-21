package com.b2b.trade.repository;

import com.b2b.trade.entity.Transaction;
import com.b2b.trade.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;
import java.util.UUID;

public interface TransactionRepository extends JpaRepository<Transaction, UUID> {
    List<Transaction> findByExporter(User exporter);

    @Query("SELECT t FROM Transaction t WHERE t.exporter = :exporter")
    List<Transaction> findAllByExporter(@Param("exporter") User exporter);
}