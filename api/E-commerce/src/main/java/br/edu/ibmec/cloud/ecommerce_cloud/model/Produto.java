package br.edu.ibmec.cloud.ecommerce_cloud.model;

import com.azure.spring.data.cosmos.core.mapping.Container;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;
import jakarta.persistence.Id;
import lombok.Data;

import java.util.List;

@Data
@Container(containerName = "produtos")
public class Produto {

    @Id
    private String id;

    @PartitionKey
    private String produtoCategoria;

    private String produtoNome;

    private double preco;

    private List<String> imageUrl;

    private String produtoDescrisao;
}
