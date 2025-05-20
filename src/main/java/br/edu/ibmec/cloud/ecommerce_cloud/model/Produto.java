package br.edu.ibmec.cloud.ecommerce_cloud.model;

import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Data;

import java.util.List;

@Data
@Container(containerName = "produtos")
public class Produto {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String id;

    @PartitionKey
    private String produtoCategoria;

    private String produtoNome;

    private double preco;

    private List<String> imageUrl;

    private String produtoDescrisao;
}
