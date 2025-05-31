package br.edu.ibmec.cloud.ecommerce_cloud.request;

import lombok.Data;

@Data
public class ItemRequest {
    private String produtoId;
    private int quantidade;
}
