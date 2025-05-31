package br.edu.ibmec.cloud.ecommerce_cloud.model;


import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;

@Data
@Container(containerName = "pedidos")
public class Pedido {

    @Id
    private String id;

    @PartitionKey
    private String usuarioId;

    private LocalDateTime dataPedido;

    private List<ItemPedido> itens;

    private Endereco enderecoEntrega;

    private double valorTotal;

    private String status;

    private String transacaoId;

}
