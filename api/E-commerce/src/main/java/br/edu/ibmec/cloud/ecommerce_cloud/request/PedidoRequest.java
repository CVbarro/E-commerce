package br.edu.ibmec.cloud.ecommerce_cloud.request;

import br.edu.ibmec.cloud.ecommerce_cloud.model.Endereco;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;

@Data
public class PedidoRequest {
    private int usuarioId;
    private List<ItemRequest> itens;
    private Endereco endereco;
    private String numeroCartao;
    private String cvv;
    private LocalDateTime dtExpiracao;
}
