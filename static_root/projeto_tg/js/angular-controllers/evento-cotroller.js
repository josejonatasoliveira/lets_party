angular.module("myApp", ['ngSanitize'])
  .controller("myCtrl", function($scope) {
  
    $scope.quillDataJSON = "init";
    $scope.quillDataText = "init";
    $scope.quillDataHTML = "init";
  
    $scope.quillData = "hahaha";
    $scope.quillConfig = "hahaConfig";
  
    $scope.changeData = function() {
      $scope.quillData = "config";   
    };
  
    $scope.clickMe = function() {
      alert("thanks!");
    };
  })
  .directive('quillEditor', function($compile) {
    return {
      restrict: 'E',
      // for now shared scope
      // TODO: find a way to get attributes from directive with shared scope
      
      // scope: {
      //    // passed directive data
      //     quillData: '=',
      //     quillConfig: '='
      // },
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
            
            console.log(JSON.stringify(delta));
            
            // THIS WOULD NOT WORK WITHOUT SCOPE.APPLY
            $scope.$apply(function() {
              console.log("ha");
              console.log($scope);
              $scope.quillDataJSON = JSON.stringify(delta);
              $scope.quillDataText = text;
              $scope.quillDataHTML = justHtml;
            });
          });
      },
      
      // transclude: true,
      // template: '<div class="well"><h3>Template content</h3><div ng-transclude></div></div>'
      // template: '<div id="editor">' +
      //               '<p>Hello World!</p>' +
      //               '<p>Some initial <strong>bold</strong> text</p>' +
      //               '<p><br></p>'
      //         '</div>';
    };
  });