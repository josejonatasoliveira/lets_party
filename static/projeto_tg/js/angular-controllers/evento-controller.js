angular.module("myApp", ['ngSanitize'])
  .controller("myCtrl", function($scope) {
  
    $scope.quillDataJSON = "init";
    $scope.quillDataText = "init";
    $scope.quillDataHTML = "init";
  
    $scope.quillData = "hahaha";
    $scope.quillConfig = "hahaConfig";

    $scope.message = "";
  
    $scope.changeData = function() {
      $scope.quillData = "config";   
    };
  
    var editor =CKEDITOR.replace( 'editor_1' );
    CKEDITOR.config.extraPlugins = "base64image";
    $("#save_event").on('submit', (e) => {
      $("#id_description").attr('value',editor.getData())
    })


    getCity = (e) =>{

      input = document.getElementById('id_city');
      debugger;
      children_element = input.children;

      if (children_element.length > 0){
        input.innerHTML = ""; 
      }

      $.ajax({
        url: 'search_for/city/', 
        data: {
          'sigla': e.value
        }, 
        success: function(data) {
          data.results.forEach((el) => {
            var ul = `<li class="mdl-menu__item" data-val="${ el }">${ el }</li>`
            input.innerHTML = input.innerHTML + ul;
          })
        }
      })
    
    }

    $('#id_image_file').change(function(e){
      var res=$('#id_image_file').val();
      var arr = res.split("\\");
      var filename=arr.slice(-1)[0];
      filextension=filename.split(".");
      filext="."+filextension.slice(-1)[0];
      valid=[".jpg",".png",".jpeg",".bmp"];
      
      if (valid.indexOf(filext.toLowerCase())==-1){
        $('#id_image_file').addClass('is-invalid');
      }else{
        $('#id_image_file').removeClass('is-invalid');
      }
    });  

    function readFile() {
  
      if (this.files && this.files[0]) {
        
        var FR= new FileReader();
        
        FR.addEventListener("load", function(e) {
          $("#image_preview").attr('src', e.target.result);
          $('#image_preview').css('background-image', `url(${ e.target.result })`);
        }); 
        
        FR.readAsDataURL( this.files[0] );
      }
      
    }
    
    document.getElementById("id_image_file").addEventListener("change", readFile);

  })
  .directive('quillEditor', function($compile) {
    return {
      restrict: 'E',

      link: function($scope, $element) {
           var template= '<div id="editor">' +
                    '<p>Hello World!</p>' +
                    '<p>Some initial <strong>bold</strong> text</p>' +
                    '<p><br></p>'
              '</div>';
          var linkFunc = $compile(template);
          var content = linkFunc($scope);
          $element.append(content);
        
          // setup quill config after adding to DOM
          var quill = new Quill('#editor', {
            modules: {
              // ImageResize: {},
              toolbar: [
                [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                // [{ 'header': 1 }, { 'header': 2 }],
                [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
                ['bold', 'italic', 'underline', 'strike', 'link'],
                [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
                [{ 'font': [] }],
                [{ 'align': [] }],
                ['clean'],                                         // remove formatting button
                ['blockquote', 'code-block'],
                ['video', 'image'],
                [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
                [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
              ]
            },
            placeholder: 'Compose an epic...',
            theme: 'snow'  // or 'bubble'
          });

          quill.on('text-change', function() {
            var delta = quill.getContents();
            var text = quill.getText();
            var justHtml = quill.root.innerHTML;
            debugger;
            // THIS WOULD NOT WORK WITHOUT SCOPE.APPLY
            $scope.$apply(function() {

              $scope.quillDataJSON = JSON.stringify(delta);
              $scope.quillDataText = text;
              $scope.quillDataHTML = justHtml;
            });
          });
      },
      
    };
  });