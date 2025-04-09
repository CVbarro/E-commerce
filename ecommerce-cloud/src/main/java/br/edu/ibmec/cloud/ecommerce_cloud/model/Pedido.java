package br.edu.ibmec.cloud.ecommerce_cloud.model;

import com.azure.spring.data.cosmos.core.mapping.PartitionKey;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.List;

@Data
@Component
public class Pedido {

    @Id
    private String id;

    @PartitionKey
    private String customerId; // Ex: ID do cliente que fez o pedido

    private LocalDateTime orderDate; // Data do pedido
    private List<Produto> produtos;  // Lista de produtos no pedido
    private double totalAmount;      // Valor total do pedido
}