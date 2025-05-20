package br.edu.ibmec.cloud.ecommerce_cloud.controller;

import br.edu.ibmec.cloud.ecommerce_cloud.model.Cartao;
import br.edu.ibmec.cloud.ecommerce_cloud.model.Usuario;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import br.edu.ibmec.cloud.ecommerce_cloud.repository.CartaoRepository;
import br.edu.ibmec.cloud.ecommerce_cloud.repository.UsuarioRepository;
import br.edu.ibmec.cloud.ecommerce_cloud.request.TransacaoRequest;
import br.edu.ibmec.cloud.ecommerce_cloud.request.TransacaoResponse;

import java.time.LocalDateTime;
import java.util.Iterator;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/cartao/{id_user}")
public class CartaoController {

    @Autowired
    private CartaoRepository cartaoRepository;

    @Autowired
    private UsuarioRepository usuarioRepository;

    @PostMapping
    public ResponseEntity<Cartao> create(@PathVariable("id_user") int id_user, @RequestBody Cartao cartao) {
        Optional<Usuario> optionalUsuario = usuarioRepository.findById(id_user);

        if (optionalUsuario.isEmpty())
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);

        Usuario usuario = optionalUsuario.get();


        usuario.getCartoes().add(cartao);
        cartaoRepository.save(cartao);
        usuarioRepository.save(usuario);

        return new ResponseEntity<>(cartao, HttpStatus.CREATED);
    }

    @DeleteMapping
    public ResponseEntity<Void> delete(@PathVariable("id_user") int id_user, @RequestBody Cartao cartao) {
        Optional<Usuario> optionalUsuario = usuarioRepository.findById(id_user);

        if (optionalUsuario.isEmpty()) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        Usuario usuario = optionalUsuario.get();
        Iterator<Cartao> iterator = usuario.getCartoes().iterator();
        boolean cartaoEncontrado = false;

        while (iterator.hasNext()) {
            Cartao c = iterator.next();
            if (Objects.equals(c.getNumero(),cartao.getNumero())) {
                iterator.remove();
                cartaoEncontrado = true;
                break;
            }
        }

        if (!cartaoEncontrado) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        usuarioRepository.save(usuario);

        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @PostMapping("/authorize")
    public ResponseEntity<TransacaoResponse> authorize(@PathVariable("id_user") int id_user, @RequestBody TransacaoRequest request) {
        Optional<Usuario> optionalUsuario = usuarioRepository.findById(id_user);

        if (optionalUsuario.isEmpty())
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);

        Usuario usuario = optionalUsuario.get();
        Cartao cartaoCompra = usuario.getCartoes().stream()
                .filter(c -> c.getNumero().equals(request.getNumero()) && c.getCvv().equals(request.getCvv()))
                .findFirst()
                .orElse(null);

        if (cartaoCompra == null) {
            return criarRespostaTransacao("NOT_AUTHORIZED", "Cartão não encontrado para o usuário", HttpStatus.NOT_FOUND);
        }

        if (cartaoCompra.getDtExpiracao().isBefore(LocalDateTime.now())) {
            return criarRespostaTransacao("NOT_AUTHORIZED", "Cartão Expirado", HttpStatus.BAD_REQUEST);
        }

        if (cartaoCompra.getSaldo() < request.getValor()) {
            return criarRespostaTransacao("NOT_AUTHORIZED", "Sem saldo para realizar a compra", HttpStatus.BAD_REQUEST);
        }

        // Debita o valor da compra
        cartaoCompra.setSaldo(cartaoCompra.getSaldo() - request.getValor());
        cartaoRepository.save(cartaoCompra);

        return criarRespostaTransacao("AUTHORIZED", "Compra autorizada", HttpStatus.OK);
    }

    private ResponseEntity<TransacaoResponse> criarRespostaTransacao(String status, String mensagem, HttpStatus httpStatus) {
        TransacaoResponse response = new TransacaoResponse();
        response.setStatus(status);
        response.setDtTransacao(LocalDateTime.now());
        response.setMessage(mensagem);
        if ("AUTHORIZED".equals(status)) {
            response.setCodigoAutorizacao(UUID.randomUUID());
        }
        return new ResponseEntity<>(response, httpStatus);
    }
}
