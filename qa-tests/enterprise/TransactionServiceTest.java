import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

public class TransactionServiceTest {
    @Mock
    private TransactionRepository transactionRepository;

    @InjectMocks
    private TransactionService transactionService;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testGetTransactionsByLeadId() {
        UUID leadId = UUID.randomUUID();
        List<Transaction> transactions = List.of(new Transaction(), new Transaction());
        when(transactionRepository.findByLeadId(leadId)).thenReturn(transactions);

        List<Transaction> result = transactionService.getTransactionsByLeadId(leadId);

        assertEquals(transactions, result);
    }

    @Test
    public void testSaveTransaction() {
        Transaction transaction = new Transaction();
        when(transactionRepository.save(any(Transaction.class))).thenReturn(transaction);

        Transaction savedTransaction = transactionService.saveTransaction(transaction);

        assertEquals(transaction, savedTransaction);
    }
}
