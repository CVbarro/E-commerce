package br.edu.ibmec.cloud.ecommerce_cloud.controller;

import br.edu.ibmec.cloud.ecommerce_cloud.model.*;
import br.edu.ibmec.cloud.ecommerce_cloud.repository.UsuarioRepository;
import br.edu.ibmec.cloud.ecommerce_cloud.repository.cosmos.PedidoRepository;
import br.edu.ibmec.cloud.ecommerce_cloud.repository.cosmos.ProdutoRepository;
import br.edu.ibmec.cloud.ecommerce_cloud.request.ItemRequest;
import br.edu.ibmec.cloud.ecommerce_cloud.request.PedidoRequest;
import br.edu.ibmec.cloud.ecommerce_cloud.request.TransacaoRequest;
import br.edu.ibmec.cloud.ecommerce_cloud.request.TransacaoResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/pedidos")
public class PedidoController {

    @Autowired
    private UsuarioRepository usuarioRepository;

    @Autowired
    private ProdutoRepository produtoRepository;

    @Autowired
    private PedidoRepository pedidoRepository;

    @Autowired
    private CartaoController cartaoController;

    @PostMapping
    public ResponseEntity<?> criarPedido(@RequestBody PedidoRequest request) {
        // 1. Validar usuário
        Optional<Usuario> usuarioOptional = usuarioRepository.findById(request.getUsuarioId());
        if (usuarioOptional.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Usuário não encontrado");
        }

        Usuario usuario = usuarioOptional.get();

        // 2. Validar endereço enviado
        Endereco endereco = request.getEndereco();
        if (endereco == null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Endereço é obrigatório");
        }

        // 3. Montar itens do pedido e calcular total
        List<ItemPedido> itens = new ArrayList<>();
        double total = 0.0;

        for (ItemRequest item : request.getItens()) {
            Optional<Produto> produtoOpt = produtoRepository.findById(item.getProdutoId());
            if (produtoOpt.isEmpty()) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Produto " + item.getProdutoId() + " não encontrado");
            }

            Produto produto = produtoOpt.get();

            ItemPedido itemPedido = new ItemPedido();
            itemPedido.setProdutoId(produto.getId());
            itemPedido.setNomeProduto(produto.getProdutoNome());
            itemPedido.setPrecoUnitario(produto.getPreco());
            itemPedido.setQuantidade(item.getQuantidade());

            itens.add(itemPedido);
            total += produto.getPreco() * item.getQuantidade();
        }

        // 4. Autorizar pagamento via CartaoController
        TransacaoRequest txRequest = new TransacaoRequest();
        txRequest.setNumero(request.getNumeroCartao());
        txRequest.setCvv(request.getCvv());
        txRequest.setDtExpiracao(request.getDtExpiracao());
        txRequest.setValor(total);

        ResponseEntity<TransacaoResponse> txResponse = cartaoController.authorize(request.getUsuarioId(), txRequest);

        if (!txResponse.getStatusCode().is2xxSuccessful() || !"AUTHORIZED".equals(txResponse.getBody().getStatus())) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(txResponse.getBody());
        }

        // 5. Criar Pedido no Cosmos DB
        Pedido pedido = new Pedido();
        pedido.setId(UUID.randomUUID().toString());
        pedido.setUsuarioId(String.valueOf(request.getUsuarioId()));
        pedido.setDataPedido(LocalDateTime.now());
        pedido.setItens(itens);
        pedido.setEnderecoEntrega(endereco); // endereço enviado no JSON
        pedido.setValorTotal(total);
        pedido.setStatus("AUTORIZADO");
        pedido.setTransacaoId(txResponse.getBody().getCodigoAutorizacao().toString());

        pedidoRepository.save(pedido);

        return ResponseEntity.status(HttpStatus.CREATED).body(pedido);
    }

    @GetMapping
    public ResponseEntity<List<Pedido>> listarTodosPedidos() {
        List<Pedido> pedidos = new ArrayList<>();
        pedidoRepository.findAll().forEach(pedidos::add);
        return ResponseEntity.ok(pedidos);
    }

    @GetMapping("/usuario/{usuarioId}")
    public ResponseEntity<List<Pedido>> listarPedidosPorUsuario(@PathVariable String usuarioId) {
        Iterable<Pedido> todos = pedidoRepository.findAll();
        List<Pedido> doUsuario = new ArrayList<>();

        for (Pedido pedido : todos) {
            if (pedido.getUsuarioId() != null && pedido.getUsuarioId().equals(usuarioId)) {
                doUsuario.add(pedido);
            }
        }

        return ResponseEntity.ok(doUsuario);
    }

    @DeleteMapping("/{usuarioId}/{pedidoId}")
    public ResponseEntity<Void> delete(@PathVariable("usuarioId") String usuarioId, @PathVariable String pedidoId) {
        Optional<Pedido> pedidoOptional = pedidoRepository.findById(pedidoId);
        if (pedidoOptional.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        Pedido existente = pedidoOptional.get();

        if (!existente.getUsuarioId().equals(usuarioId)) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        }

        pedidoRepository.delete(existente);
        return ResponseEntity.noContent().build();
    }
}