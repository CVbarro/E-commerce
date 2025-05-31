package br.edu.ibmec.cloud.ecommerce_cloud.model;

import com.azure.spring.data.cosmos.core.mapping.Container;
import jakarta.persistence.GeneratedValue;
import com.azure.spring.data.cosmos.core.mapping.PartitionKey;
import jakarta.persistence.GenerationType;
import lombok.Data;
import org.springframework.data.annotation.Id;

import java.util.List;

@Data
@Container(containerName = "products")
public class Produto {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String id;

    @PartitionKey
    private String productCategory;

    private String productName;

    private double price;

    private List<String> imageUrl;

    private String productDescription;



}