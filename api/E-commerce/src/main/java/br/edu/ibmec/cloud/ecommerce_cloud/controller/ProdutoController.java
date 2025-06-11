package br.edu.ibmec.cloud.ecommerce_cloud.controller;

import br.edu.ibmec.cloud.ecommerce_cloud.dtos.CreateProductDto;
import br.edu.ibmec.cloud.ecommerce_cloud.model.Produto;
import br.edu.ibmec.cloud.ecommerce_cloud.repository.cosmos.ProdutoRepository;
import br.edu.ibmec.cloud.ecommerce_cloud.services.AzureBlobService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import java.util.stream.Collectors;
import com.fasterxml.jackson.databind.ObjectMapper;


import java.io.IOException;
import java.util.*;

@RestController
@RequestMapping("/produtos")
public class ProdutoController {

    @Autowired
    private ProdutoRepository repository;

    @Autowired
    private AzureBlobService azureBlobService;


    @PostMapping(value = "", consumes = "multipart/form-data")
    public ResponseEntity<Produto> create(
            @RequestPart("produto") String produtoJson,
            @RequestParam Map<String, MultipartFile> arquivosForm) {

        try {
            // Converte o JSON string para DTO
            ObjectMapper mapper = new ObjectMapper();
            CreateProductDto dto = mapper.readValue(produtoJson, CreateProductDto.class);

            Produto produto = new Produto();
            produto.setId(UUID.randomUUID().toString());
            produto.setProdutoNome(dto.getProdutoNome());
            produto.setProdutoCategoria(dto.getProdutoCategoria());
            produto.setPreco(dto.getPreco());
            produto.setProdutoDescrisao(dto.getDescricao());

            List<String> imageUrls = new ArrayList<>();
            for (Map.Entry<String, MultipartFile> entry : arquivosForm.entrySet()) {
                if (entry.getKey().startsWith("imagem") && !entry.getValue().isEmpty()) {
                    String url = azureBlobService.uploadFile(entry.getValue());
                    imageUrls.add(url);
                }
            }

            produto.setImageUrl(imageUrls);
            repository.save(produto);
            return new ResponseEntity<>(produto, HttpStatus.CREATED);

        } catch (IOException e) {
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        }
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
        List<Produto> result = new ArrayList<>();
        repository.findAll().forEach(result::add);
        List<Produto> produtosEncontrados = result.stream()
                .filter(p -> p.getProdutoNome() != null &&
                        p.getProdutoNome().toLowerCase().contains(produtoNome.toLowerCase()))
                .collect(Collectors.toList());

        return new ResponseEntity<>(produtosEncontrados, HttpStatus.OK);
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
