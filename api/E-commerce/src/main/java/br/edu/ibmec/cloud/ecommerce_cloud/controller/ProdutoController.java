package br.edu.ibmec.cloud.ecommerce_cloud.controller;

import br.edu.ibmec.cloud.ecommerce_cloud.model.Produto;
import br.edu.ibmec.cloud.ecommerce_cloud.repository.cosmos.ProdutoRepository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/produtos")
public class ProdutoController {

    @Autowired
    private ProdutoRepository repository;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ResponseEntity<Produto> create(@RequestBody Produto produto){

        produto.setId(UUID.randomUUID().toString());
        repository.save(produto);

        return new ResponseEntity<>(produto, HttpStatus.CREATED);
    }

    @GetMapping("{id}")
    public ResponseEntity<Produto> get(@PathVariable String id) {
        Optional<Produto> optionalProduto = this.repository.findById(id);
        return optionalProduto
                .map(produto -> new ResponseEntity<>(produto, HttpStatus.OK))
                .orElseGet(() -> new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }

    @GetMapping("/procurar")
    public ResponseEntity<Iterable<Produto>> getProdutoPorNome(@RequestParam("produtoNome") String produtoNome) {
        Optional<List<Produto>> optionalProduto = this.repository.findByProdutoNomeContains(produtoNome);

        if (optionalProduto.isEmpty()) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        return new ResponseEntity<>(optionalProduto.get(), HttpStatus.OK);
    }


    @GetMapping
    public ResponseEntity<Iterable<Produto>> getAll() {
        List<Produto> result = new ArrayList<>();
        repository.findAll().forEach(result::add);
        return new ResponseEntity<>(result, HttpStatus.OK);
    }

    @PutMapping("{id}")
    public ResponseEntity<Produto> atualizar(@PathVariable String id, @RequestBody Produto produtoAtualizado) {
        Optional<Produto> optionalProduto = this.repository.findById(id);

        if (optionalProduto.isEmpty()) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        Produto produtoExistente = optionalProduto.get();
        produtoExistente.setProdutoNome(produtoAtualizado.getProdutoNome());
        produtoExistente.setProdutoCategoria(produtoAtualizado.getProdutoCategoria());
        produtoExistente.setPreco(produtoAtualizado.getPreco());
        produtoExistente.setImageUrl(produtoAtualizado.getImageUrl());
        produtoExistente.setProdutoDescrisao(produtoAtualizado.getProdutoDescrisao());

        Produto produtoSalvo = this.repository.save(produtoExistente);
        return new ResponseEntity<>(produtoSalvo, HttpStatus.OK);
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
}
