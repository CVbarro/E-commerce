package controller;

import models.Endereco;
import models.Usuario;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import repository.EnderecoRepository;
import repository.UsuarioRepository;

import java.util.Optional;

@RestController
@RequestMapping("/address/{id_user}")
public class EnderecoController {
    @Autowired
    private EnderecoRepository enderecoRepository;

    @Autowired
    private UsuarioRepository usuarioRepository;

    @PostMapping
    public ResponseEntity<Endereco> create(@PathVariable("id_user") int id_user, @RequestBody Endereco endereco) {
        //Verificando se o usuario existe na base
        Optional<Usuario> optionalUsuario = this.usuarioRepository.findById(id_user);

        if (optionalUsuario.isEmpty())
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);

        //Cria o endereco  na base
        enderecoRepository.save(endereco);

        //Associa o endereco ao usuario
        Usuario usuario = optionalUsuario.get();

        usuario.getEnderecos().add(endereco);
        usuarioRepository.save(usuario);

        return new ResponseEntity<>(endereco, HttpStatus.CREATED);

    }

    @DeleteMapping
    public ResponseEntity<Void> delete(@PathVariable("id_user") int id_user, @RequestBody Endereco endereco){
        Optional<Usuario> optionalUsuario = this.usuarioRepository.findById(id_user);

        //verifica o usuario
        if (optionalUsuario.isEmpty())
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);

        Usuario usuario = optionalUsuario.get();

        //verifica se o usuario tem endereco
        if (!usuario.getEnderecos().contains(endereco))
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);

        //remove o endereco do usuario
        usuario.getEnderecos().remove(endereco);
        usuarioRepository.save(usuario);

        return new ResponseEntity<>(HttpStatus.NO_CONTENT);

    }

}
