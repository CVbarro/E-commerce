package br.edu.ibmec.cloud.ecommerce_cloud.controller;


import br.edu.ibmec.cloud.ecommerce_cloud.model.Produto;
import br.edu.ibmec.cloud.ecommerce_cloud.repository.cosmos.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;



@RestController
@RequestMapping("/products")
public class ProdutoController {

    @Autowired
    private ProductRepository repository;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ResponseEntity<Produto> create(@RequestBody Produto product) {
        repository.save(product);
        return new ResponseEntity<>(product, HttpStatus.CREATED);
    }

    @GetMapping("{id}")
    public ResponseEntity<Produto> get(@PathVariable String id) {
        Optional<Produto> optionalProduto = this.repository.findById(id);
        return optionalProduto
                .map(produto -> new ResponseEntity<>(produto, HttpStatus.OK))
                .orElseGet(() -> new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }

    @GetMapping
    public ResponseEntity<Iterable<Produto>> getAll() {
        List<Produto> result = new ArrayList<>();
        repository.findAll().forEach(result::add);
        return new ResponseEntity<>(result, HttpStatus.OK);
    }

    @DeleteMapping("{id}")
    public ResponseEntity<Void> delete(@PathVariable String id) {
        Optional<Produto> optionalProduto = this.repository.findById(id);
        if (optionalProduto.isEmpty()) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        this.repository.delete(optionalProduto.get());
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }



    @PostMapping("/produto")
    public ResponseEntity<Produto> criar(@RequestBody Produto produto) {
        Produto novoProduto = this.repository.save(produto);
        return new ResponseEntity<>(novoProduto, HttpStatus.CREATED);
    }

    @PutMapping("/produto/{id}")
    public ResponseEntity<Produto> atualizar(@PathVariable String id, @RequestBody Produto produtoAtualizado) {
        Optional<Produto> optionalProduto = this.repository.findById(id);

        if (optionalProduto.isEmpty()) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        Produto produtoExistente = optionalProduto.get();
        produtoExistente.setProductName(produtoAtualizado.getProductName());
        produtoExistente.setProductCategory(produtoAtualizado.getProductCategory());
        produtoExistente.setPrice(produtoAtualizado.getPrice());
        produtoExistente.setImageUrl(produtoAtualizado.getImageUrl());
        produtoExistente.setProductDescription(produtoAtualizado.getProductDescription());

        Produto produtoSalvo = this.repository.save(produtoExistente);
        return new ResponseEntity<>(produtoSalvo, HttpStatus.OK);
    }
}
