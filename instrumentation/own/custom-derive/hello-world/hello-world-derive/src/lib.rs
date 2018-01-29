extern crate proc_macro;
extern crate syn;
#[macro_use]
extern crate quote;

use proc_macro::TokenStream;
use syn::DeriveInput;
use syn::Attribute;

#[proc_macro_derive(HelloWorld, attributes(opcode))]
pub fn hello_world(input: TokenStream) -> TokenStream {
    // Parse the input tokens into a syntax tree
    let input: DeriveInput = syn::parse(input).unwrap();

    let attrs: Vec<Option<syn::Meta>> = input.attrs.iter().map(Attribute::interpret_meta).collect();

    println!("{:?}", attrs);

    // Build the impl
    let name = input.ident;
    let expanded = quote! {
        impl HelloWorld for #name {
            fn hello_world() {
                println!("My name is {}", stringify!(#name));
            }
        }
    };

    // Return the generated impl
    expanded.into()
}