package br.edu.ibmec.cloud.ecommerce_cloud.controller;

import br.edu.ibmec.cloud.ecommerce_cloud.model.Pedido;
import br.edu.ibmec.cloud.ecommerce_cloud.repository.cosmos.PedidoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/api/pedidos")
public class PedidoController {

    @Autowired
    private PedidoRepository repository;

    // LISTAR todos os pedidos
    @GetMapping
    public ResponseEntity<Iterable<Pedido>> listarTodos() {
        Iterable<Pedido> pedidos = this.repository.findAll();
        return new ResponseEntity<>(pedidos, HttpStatus.OK);
    }

    // CRIAR novo pedido
    @PostMapping
    public ResponseEntity<Pedido> criar(@RequestBody Pedido novoPedido) {
        Pedido pedidoSalvo = this.repository.save(novoPedido);
        return new ResponseEntity<>(pedidoSalvo, HttpStatus.CREATED);
    }

    // ATUALIZAR pedido existente
    @PutMapping("/{id}")
    public ResponseEntity<Pedido> atualizar(@PathVariable String id, @RequestBody Pedido pedidoAtualizado) {
        Optional<Pedido> optionalPedido = this.repository.findById(id);

        if (optionalPedido.isEmpty()) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        Pedido pedidoExistente = optionalPedido.get();
        pedidoExistente.setCustomerId(pedidoAtualizado.getCustomerId());
        pedidoExistente.setOrderDate(pedidoAtualizado.getOrderDate());
        pedidoExistente.setProdutos(pedidoAtualizado.getProdutos());
        pedidoExistente.setTotalAmount(pedidoAtualizado.getTotalAmount());

        Pedido pedidoSalvo = this.repository.save(pedidoExistente);
        return new ResponseEntity<>(pedidoSalvo, HttpStatus.OK);
    }

    // DELETAR pedido
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletar(@PathVariable String id) {
        Optional<Pedido> optionalPedido = this.repository.findById(id);

        if (optionalPedido.isEmpty()) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        this.repository.delete(optionalPedido.get());
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
}
