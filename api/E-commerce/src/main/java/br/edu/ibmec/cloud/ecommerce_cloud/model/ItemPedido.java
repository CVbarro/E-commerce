package br.edu.ibmec.cloud.ecommerce_cloud.model;

import lombok.Data;

@Data
public class ItemPedido {

    private String produtoId;
    private String nomeProduto;
    private double precoUnitario;
    private int quantidade;

}
