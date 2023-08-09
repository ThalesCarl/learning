pub trait Draw {
    fn draw(&self);
}

pub struct Screen {
    // Box<dyn Draw> is a trait object that can hold any type that implements the Draw trait
    pub components: Vec<Box<dyn Draw>>, 
}

impl Screen {
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw()
        }
    }
}

pub struct Button {
    pub width: u32,
    pub height: u32,
    pub label: String,
}

impl Draw for Button {
    fn draw(&self) {
        println!("Drawing button with label = {}, width = {}, heigth = {}", self.label, self.width, self.height);
    }
}

pub struct SelectBox {
    pub width: u32,
    pub height: u32,
    pub options: Vec<String>,
}

impl Draw for SelectBox {
    fn draw(&self) {
        println!("Drawing selectbox with width = {}, height = {}", self.width, self.height);
    }
}
