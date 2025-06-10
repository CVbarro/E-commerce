package br.edu.ibmec.cloud.ecommerce_cloud.dtos;

import lombok.Data;

@Data
public class CreateProductDto {
    private String produtoNome;
    private String produtoCategoria;
    private String descricao;
    private Double preco;
    private Integer estoque;
}
