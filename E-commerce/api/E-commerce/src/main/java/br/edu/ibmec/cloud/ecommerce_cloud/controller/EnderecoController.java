package br.edu.ibmec.cloud.ecommerce_cloud.controller;

import br.edu.ibmec.cloud.ecommerce_cloud.model.Endereco;
import br.edu.ibmec.cloud.ecommerce_cloud.model.Usuario;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import br.edu.ibmec.cloud.ecommerce_cloud.repository.EnderecoRepository;
import br.edu.ibmec.cloud.ecommerce_cloud.repository.UsuarioRepository;

import java.util.Iterator;
import java.util.Objects;
import java.util.Optional;

@RestController
@RequestMapping("/endereco/{id_user}")
public class EnderecoController {
    @Autowired
    private EnderecoRepository enderecoRepository;

    @Autowired
    private UsuarioRepository usuarioRepository;

    @PostMapping
    public ResponseEntity<Endereco> create(@PathVariable("id_user") int id_user, @RequestBody Endereco endereco) {
        Optional<Usuario> optionalUsuario = usuarioRepository.findById(id_user);

        if (optionalUsuario.isEmpty())
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);

        Usuario usuario = optionalUsuario.get();

        // Associa o endereço ao usuário antes de salvar
        usuario.getEnderecos().add(endereco);
        enderecoRepository.save(endereco);  // Agora sim, salva no banco
        usuarioRepository.save(usuario);    // Salva o usuário atualizado

        return new ResponseEntity<>(endereco, HttpStatus.CREATED);
    }

    @DeleteMapping // Removemos o "/{id_user}" porque já está definido no @RequestMapping
    public ResponseEntity<Void> delete(@PathVariable("id_user") int id_user, @RequestBody Endereco endereco) {
        Optional<Usuario> optionalUsuario = usuarioRepository.findById(id_user);

        if (optionalUsuario.isEmpty())
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);

        Usuario usuario = optionalUsuario.get();
        Iterator<Endereco> iterator = usuario.getEnderecos().iterator();
        boolean enderecoEncontrado = false;

        while (iterator.hasNext()) {
            Endereco e = iterator.next();
            if (Objects.equals(e.getCep(), endereco.getCep())) {
                iterator.remove();
                enderecoEncontrado = true;
                break;
            }
        }

        if (!enderecoEncontrado) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        usuarioRepository.save(usuario); // Salva a lista de endereços atualizada

        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
}
