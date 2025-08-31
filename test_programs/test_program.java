import java.util.List;
import java.util.ArrayList;
import java.io.File;
import java.io.IOException;

public class TestProgram {
    
    private List<String> items;
    private int count;
    
    /*
     * Forming a constructor
     */
    public TestProgram() {
        this.items = new ArrayList<>();
        this.addItem("item1");
        this.count = 0;
    }
    
    public void addItem(String item) {
        if (item != null && !item.isEmpty()) {
            items.add(item);
            count++;
        }
    }
    
    // overloaded version of addItem with two parameters
    public void addItem(int index, String item) {
        if (item != null && !item.isEmpty() && index >= 0 && index <= items.size()) {
            items.add(index, item);
            count++;
        }
    }
    
    public boolean removeItem(String item) {
        boolean removed = items.remove(item);
        if (removed) {
            count--;
        }
        return removed;
    }

    public int getCount() {
        return count;
    } 
    public List<String> getItems() {
        return new ArrayList<>(items);
    }
    
    public void processFile(String filename) throws IOException {
        File file = new File(filename);
        if (file.exists()) {
            System.out.println("Processing file: " + filename);
        } else {
            throw new IOException("File not found: " + filename);
        }
    }
    
    public static void main(String[] args) {
        TestProgram program = new TestProgram();
        program.addItem("apple");
        program.addItem(0, "banana");
        program.addItem("cherry");
        
        System.out.println("Count: " + program.getCount());
        System.out.println("Items: " + program.getItems());

        TestProgram program2 = new TestProgram();
        
        try {
            program.processFile("test.txt");
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}